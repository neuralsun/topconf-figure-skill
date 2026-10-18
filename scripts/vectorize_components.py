"""Convert selected illustration/icon regions to native path objects, never trace text or a whole figure."""
import argparse
from io import BytesIO
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from PIL import Image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design',type=Path,required=True)
    parser.add_argument('--components',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--python-deps',type=Path)
    parser.add_argument('--canvas',nargs=2,type=float,default=[1920,1080])
    args=parser.parse_args()
    if args.python_deps: sys.path.insert(0,str(args.python_deps.resolve()))
    import vtracer
    from svgpathtools import parse_path, CubicBezier, QuadraticBezier, Line
    design=Image.open(args.design).convert('RGB')
    specifications=json.loads(args.components.read_text(encoding='utf-8-sig'))
    sx,sy=args.canvas[0]/design.width,args.canvas[1]/design.height
    nodes,inventory=[],[]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    for spec in specifications:
        name=spec['name']; left,top,right,bottom=spec['source_box']
        # Intermediate region extraction is format conversion, not raster retouching.
        crop=design.crop((left,top,right,bottom))
        buffer=BytesIO(); crop.save(buffer,format='PNG')
        svg=vtracer.convert_raw_image_to_svg(buffer.getvalue(),img_format='png',colormode='color',hierarchical='stacked',mode='spline',filter_speckle=1,color_precision=spec.get('color_precision',6),layer_difference=spec.get('layer_difference',12),corner_threshold=65,length_threshold=3.5,max_iterations=20,splice_threshold=45,path_precision=3)
        (args.output.parent/(name+'.svg')).write_text(svg,encoding='utf-8')
        mapped=[]
        root=ET.fromstring(svg)
        for index,element in enumerate(root.findall('.//{http://www.w3.org/2000/svg}path')):
            path=parse_path(element.attrib['d'])
            fill=element.get('fill','#000000')
            translated=re.search(r'translate\(\s*([-\d.]+)[,\s]+([-\d.]+)',element.get('transform',''))
            dx,dy=(float(translated[1]),float(translated[2])) if translated else (0,0)
            try: xmin,xmax,ymin,ymax=path.bbox()
            except ValueError: continue
            # Stacked traces use light paths to mask dark base regions. Keep those
            # masks, even when their bounding box spans the entire component.
            if max(xmax-xmin,ymax-ymin)<.45: continue
            def coords(point): return [round((left+dx+point.real)*sx,4),round((top+dy+point.imag)*sy,4)]
            commands=[]
            for subpath in path.continuous_subpaths():
                commands.append(['M',*coords(subpath.start)])
                for segment in subpath:
                    if isinstance(segment,CubicBezier): commands.append(['C',*coords(segment.control1),*coords(segment.control2),*coords(segment.end)])
                    elif isinstance(segment,QuadraticBezier): commands.append(['Q',*coords(segment.control),*coords(segment.end)])
                    elif isinstance(segment,Line): commands.append(['L',*coords(segment.end)])
                    else:
                        for curve in segment.as_cubic_curves(): commands.append(['C',*coords(curve.control1),*coords(curve.control2),*coords(curve.end)])
                if subpath.isclosed(): commands.append(['Z'])
            ident=f'{name}-path-{index}'
            nodes.append({'id':ident,'type':'path','commands':commands,'fill':fill,'stroke':'none','z':spec.get('z',32),'group':name})
            mapped.append(ident)
        inventory.append({'name':name,'kind':spec.get('kind','icon'),'source_box':spec['source_box'],'required':True,'scene_ids':mapped})
        print(f'{name}: {len(mapped)} native curved objects',flush=True)
    args.output.write_text(json.dumps({'nodes':nodes,'component_map':inventory},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__': main()
