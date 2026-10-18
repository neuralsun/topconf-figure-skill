"""Enforce design/conversion gates; visual judgments must come from actual image review."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from export_scene import prepare, audit_files


def run(args):
    review=json.loads(args.review.read_text(encoding='utf-8-sig'))
    failures=[]
    design_hash=hashlib.sha256(args.design.read_bytes()).hexdigest()
    if review.get('design_sha256')!=design_hash:
        failures.append('Review is not bound to this exact design image.')
    criteria=('reference_comparison_done','scientific_content_correct','no_global_title_or_caption','readable','rich_visual_objects_preserved')
    design_review=review.get('design_review',{})
    for key in criteria:
        if design_review.get(key) is not True:
            failures.append('Design criterion failed or not reviewed: '+key)
    if design_review.get('quality_score',0)<8:
        failures.append('Design visual review score is below 8/10.')
    failures.extend('Design issue: '+str(issue) for issue in design_review.get('issues',[]))
    report={'stage':args.stage,'design_sha256':design_hash,'design_image':str(args.design.resolve()),'visual_review_is_model_assisted_not_an_automatic_aesthetic_metric':True,'failures':failures}
    if failures:
        report['status']='REDESIGN_REQUIRED'
        return report
    if args.stage=='design':
        report['status']='PASS'
        return report
    if not args.scene or not args.basename:
        raise ValueError('Final stage needs --scene and --basename.')
    scene,warnings=prepare(json.loads(args.scene.read_text(encoding='utf-8-sig')))
    nodes={node['id']:node for node in scene['nodes']}
    items=review.get('component_map',[])
    if not items:
        failures.append('Missing object inventory mapped from the design.')
    for item in items:
        if item.get('required',True) and not item.get('scene_ids'):
            failures.append('Unconverted required component: '+item['name'])
        for ident in item.get('scene_ids',[]):
            if ident not in nodes:
                failures.append(f'Mapped scene object does not exist: {ident}')
    if any(n.get('role') in ('global-title','figure-caption') for n in scene['nodes']):
        failures.append('A global title or caption remains in the editable scene.')
    required=review.get('required_labels',[])
    flattened=''.join(''.join(n.get('text','').split()) for n in scene['nodes'])
    for value in required:
        if ''.join(value.split()) not in flattened:
            failures.append('Missing required label: '+value)
    conversion=review.get('conversion_review',{})
    for key in ('compared_side_by_side','layout_preserved','illustrations_preserved','icons_preserved','text_and_arrows_correct','no_unintended_occlusions','office_render_reviewed'):
        if conversion.get(key) is not True:
            failures.append('Conversion criterion failed or not reviewed: '+key)
    if conversion.get('quality_score',0)<8:
        failures.append('Conversion visual review score is below 8/10.')
    failures.extend('Conversion issue: '+str(issue) for issue in conversion.get('issues',[]))
    automated=audit_files(scene,args.basename.resolve(),warnings)
    automated['office_render_reviewed']=conversion.get('office_render_reviewed') is True
    if automated['office_render_reviewed']:
        automated['limitations']=[value for value in automated['limitations'] if 'has not been checked' not in value]
    with Image.open(args.basename.with_suffix('.png')) as image:
        automated['png_size']=list(image.size)
    report.update(automated_validations=automated,required_components=len(items),visual_review=conversion)
    report['status']='RECONSTRUCTION_REQUIRED' if failures else 'PASS'
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['design','final'],required=True)
    parser.add_argument('--design',type=Path,required=True)
    parser.add_argument('--review',type=Path,required=True)
    parser.add_argument('--scene',type=Path)
    parser.add_argument('--basename',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        report=run(args)
    except Exception as error:
        report={'stage':args.stage,'status':'RECONSTRUCTION_REQUIRED' if args.stage=='final' else 'REDESIGN_REQUIRED','failures':[str(error)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['status']=='PASS' else 2)


if __name__=='__main__':
    main()
