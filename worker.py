"""Free GitHub Actions documentary generator. Review-only; no publishing."""
import asyncio, json, math, os, random, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H,FPS=540,960,12
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TOPICS={
"universe":("The Nearest Star Beyond the Sun",[
"Imagine travelling at the speed of light, the fastest speed in the universe.",
"Even then, reaching the nearest star beyond our Sun would take more than four years.",
"That star is Proxima Centauri, about four point two four light years away.",
"A light year is a distance, not a unit of time. It is how far light travels in one year.",
"Proxima Centauri is a small red dwarf, part of the Alpha Centauri star system.",
"Space is so vast that even our nearest stellar neighbour is incredibly far away.",
"What kind of spacecraft could one day bridge that distance?"
],["https://science.nasa.gov/universe/stars/","https://science.nasa.gov/solar-system/"]),
"history":("How Roman Roads Connected an Empire",[
"Two thousand years ago, Roman engineers built roads that changed the ancient world.",
"Road crews surveyed routes, cut through terrain, and prepared stable foundations.",
"Many major roads used layers of stone, gravel, and compacted material.",
"Drainage and careful grading helped some routes withstand heavy traffic and rain.",
"These roads moved armies, merchants, officials, and messages across Roman territory.",
"Not every Roman road had the same design, and many were later rebuilt or repaired.",
"Could modern cities learn something from Roman infrastructure?"
],["https://www.britannica.com/technology/Roman-road"]),
"wars":("Why Logistics Can Decide Wars",[
"Battles may capture the headlines, but supplies often determine what armies can do.",
"Food, medicine, ammunition, and transport must reach troops when they are needed.",
"Long supply lines can become vulnerable as an army moves farther from its bases.",
"Weather, terrain, damaged bridges, and limited fuel can slow an advance.",
"History offers many examples where logistical problems shaped military campaigns.",
"Planning is not just about moving forward; it is about sustaining operations.",
"Could the outcome of a campaign change before a battle even begins?"
],["https://www.britannica.com/topic/logistics-military"]),
"evolution":("Human Evolution Was Not a Straight Line",[
"Human evolution was not a simple ladder from ape to modern human.",
"Many human relatives lived at different times, and some overlapped.",
"Fossils reveal changes in walking, tool use, teeth, and brain size.",
"Evolution branches like a tree, with populations adapting to changing environments.",
"Modern humans are one surviving branch of a much larger family history.",
"New discoveries can reshape details of this complex story.",
"What might the next fossil discovery reveal?"
],["https://humanorigins.si.edu/education/introduction-human-evolution"]),
"biology":("Why Birds and Bats Fly Differently",[
"Birds and bats both fly, but their wings evolved in different ways.",
"Bird wings are supported by modified forelimbs and covered in feathers.",
"Bat wings stretch skin between dramatically elongated fingers.",
"Both groups use muscles and aerodynamic forces to generate lift and thrust.",
"Their different structures show how evolution can solve a similar problem in distinct ways.",
"Flight requires tradeoffs in weight, manoeuvrability, and energy use.",
"Which wing design would you choose for a flying robot?"
],["https://www.britannica.com/animal/bat-mammal","https://www.britannica.com/animal/bird-animal"]),
"future":("Could Solar Sails Change Space Travel?",[
"Imagine a spacecraft moving through space without burning fuel for every push.",
"A solar sail uses the tiny momentum carried by photons from sunlight.",
"Each push is small, but the pressure can continue over long periods.",
"Solar sail missions have demonstrated the basic concept in space.",
"Future designs might help small spacecraft explore parts of the solar system.",
"Interstellar travel remains a much greater engineering challenge.",
"Could light itself help power the next generation of exploration?"
],["https://www.nasa.gov/mission/acs3/"])
}
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def wrap(draw,s,size,maxw):
    words=s.split(); lines=[]; line=""
    for word in words:
        test=(line+" "+word).strip()
        if draw.textbbox((0,0),test,font=font(size))[2]>maxw and line:
            lines.append(line); line=word
        else: line=test
    if line: lines.append(line)
    return lines
def frame(topic,title,sentence,index,frame_i,frames_per_scene):
    t=frame_i/max(1,frames_per_scene); im=Image.new("RGB",(W,H),(5,13,28)); d=ImageDraw.Draw(im)
    rng=random.Random(1729+index)
    for _ in range(95):
        x=rng.randrange(W); y=rng.randrange(H); r=rng.choice([1,1,2])
        xx=(x+int(12*math.sin(t*math.pi*2+index)))%W
        d.ellipse((xx,y,xx+r,y+r),fill=(75,106,140))
    cx=W//2+int(28*math.sin(t*math.pi*2)); cy=H//2-75
    if topic=="universe" or topic=="future":
        for radius in (160,215,280):
            d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=(26,70,111),width=2)
        r=85; d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(224,139,50))
        for k in range(8):
            angle=k*math.pi/4+t*math.pi/2
            x=cx+int(210*math.cos(angle)); y=cy+int(150*math.sin(angle))
            d.ellipse((x-6,y-6,x+6,y+6),fill=(127,212,250))
    elif topic=="biology":
        for k in range(14):
            y=270+k*29
            width=int(150*abs(math.sin(k*.4+t*1.7)))
            d.line((W//2-width,y,W//2+width,y),fill=(40+8*k,135,170),width=10)
    elif topic=="evolution":
        for k in range(7):
            x=55+k*73; y=510-int(k*23+30*math.sin(k))
            d.ellipse((x-19,y-55,x+19,y-17),fill=(60+20*k,140,160))
            d.line((x,y-16,x,y+75),fill=(60+20*k,140,160),width=13)
            d.line((x,y+70,x-20,y+112),fill=(60+20*k,140,160),width=8)
            d.line((x,y+70,x+20,y+112),fill=(60+20*k,140,160),width=8)
    else:
        for k in range(9):
            y=280+k*47
            d.polygon([(20,y),(W-20,y-40),(W-20,y-22),(20,y+18)],fill=(43+6*k,79+5*k,91))
    d.rounded_rectangle((18,26,W-18,119),radius=16,fill=(12,28,50))
    for j,line in enumerate(wrap(d,title.upper(),23,W-65)[:2]):
        d.text((W//2,45+j*29),line,font=font(23,True),anchor="mt",fill=(242,244,249))
    d.rounded_rectangle((17,680,W-17,842),radius=16,fill=(3,9,19))
    lines=wrap(d,sentence,26,W-55)
    start=715-max(0,(len(lines)-2)*17)
    for j,line in enumerate(lines[:4]):
        d.text((W//2,start+j*37),line,font=font(26,True),anchor="mt",fill=(255,255,255))
    d.text((W//2,906),"ILLUSTRATION / SIMULATION",font=font(16),anchor="mt",fill=(169,197,210))
    return im
async def voice(text,path):
    await edge_tts.Communicate(text,voice="en-US-AriaNeural",rate="-6%").save(str(path))
def duration(path):
    result=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],text=True)
    return float(result.strip())
def main():
    requested=os.environ.get("TOPIC","").lower().strip()
    topics=list(TOPICS)
    if requested not in TOPICS:
        requested=topics[(int(os.environ.get("GITHUB_RUN_NUMBER","1"))-1)%len(topics)]
    title,scenes,refs=TOPICS[requested]
    narration=" ".join(scenes)
    audio=OUT/"narration.mp3"
    asyncio.run(voice(narration,audio))
    seconds=duration(audio); totalframes=max(1,math.ceil((seconds+1.5)*FPS))
    frames_each=math.ceil(totalframes/len(scenes))
    command=["ffmpeg","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-i",str(audio),"-c:v","libx264","-preset","veryfast","-crf","25","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-shortest",str(OUT/"documentary.mp4")]
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    try:
        for i in range(totalframes):
            ix=min(len(scenes)-1,i//frames_each)
            p.stdin.write(frame(requested,title,scenes[ix],ix,i%frames_each,frames_each).tobytes())
    finally:
        p.stdin.close()
    if p.wait()!=0: raise RuntimeError("ffmpeg failed")
    metadata={"topic":requested,"title":title,"narration":narration,"references":refs,"duration_seconds":seconds,"review_required":True,"published":False,"synthetic_visuals":True,"caption":f"{title}. What surprised you most? #Documentary #Education #{requested.title()} #Science"}
    (OUT/"metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    print("REVIEW ONLY:",OUT/"documentary.mp4",f"{seconds:.1f}s")
if __name__=="__main__": main()
