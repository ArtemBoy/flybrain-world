import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x101820);
const camera=new THREE.PerspectiveCamera(60,1,.1,100);
camera.position.set(0,7,9); camera.lookAt(0,0,0);
const renderer=new THREE.WebGLRenderer({canvas:document.querySelector("#canvas"),antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
scene.add(new THREE.HemisphereLight(0xffffff,0x303030,2.2));
const floor=new THREE.Mesh(new THREE.PlaneGeometry(18,18),new THREE.MeshStandardMaterial({color:0x28323b}));
floor.rotation.x=-Math.PI/2; scene.add(floor);
scene.add(new THREE.GridHelper(18,18,0x607080,0x384550));

const agent=new THREE.Group();
const body=new THREE.Mesh(new THREE.SphereGeometry(.35,20,12),new THREE.MeshStandardMaterial({color:0xe3b341}));
body.scale.set(1,.55,1.45); agent.add(body);
const nose=new THREE.Mesh(new THREE.ConeGeometry(.14,.5,12),new THREE.MeshStandardMaterial({color:0xf0d060}));
nose.rotation.x=Math.PI/2; nose.position.z=-.55; agent.add(nose); scene.add(agent);

const target=new THREE.Mesh(new THREE.BoxGeometry(.65,.65,.65),new THREE.MeshStandardMaterial({color:0xff3030}));
target.position.y=.325; scene.add(target);

let heading=0, mode="HUMAN", brainTimer=0, brainRequestPending=false;

function reset(){
  agent.position.set(0,.35,0); heading=0; agent.rotation.y=0;
  target.position.x=2+Math.random()*3;
  target.position.z=-3+Math.random()*6;
  setMeters(null);
}

function bearing(){
  const dx=target.position.x-agent.position.x, dz=target.position.z-agent.position.z;
  const targetAngle=Math.atan2(dx,-dz);
  return Math.atan2(Math.sin(targetAngle-heading),Math.cos(targetAngle-heading));
}

function distance(){
  return Math.hypot(target.position.x-agent.position.x,target.position.z-agent.position.z);
}

function setMeters(action){
  ["left","forward","right"].forEach(x=>{
    document.querySelector("#"+x).value=x.toUpperCase()===action?1:0;
  });
}

function act(action){
  if(action==="LEFT") heading-=.12;
  if(action==="RIGHT") heading+=.12;
  if(action==="FORWARD"){
    agent.position.x+=Math.sin(heading)*.12;
    agent.position.z-=Math.cos(heading)*.12;
  }
  agent.rotation.y=heading;
  setMeters(action);
}

async function brainStep(){
  if(brainRequestPending || mode!=="BRAIN") return;
  brainRequestPending=true;
  const sensory={bearing:bearing(),distance:distance()};

  try{
    const response=await fetch("/api/act",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(sensory),
      cache:"no-store"
    });
    if(!response.ok) throw new Error(`HTTP ${response.status}`);
    const result=await response.json();
    if(mode!=="BRAIN") return;

    act(result.action);
    document.querySelector("#brain-status").textContent=
      `Python → ${result.controller}: ${result.action} · bearing ${result.bearing.toFixed(2)} rad`;
  }catch(error){
    document.querySelector("#brain-status").textContent=`Brain API error: ${error.message}`;
  }finally{
    brainRequestPending=false;
  }
}

function setMode(m){
  mode=m;
  document.querySelector("#mode").textContent=m;
  document.querySelector("#toggle").textContent=m==="HUMAN"?"Switch to BRAIN":"Switch to HUMAN";
  if(m==="HUMAN"){
    document.querySelector("#brain-status").textContent="Human control — no brain output.";
    setMeters(null);
  }else{
    document.querySelector("#brain-status").textContent="Waiting for Python BrainController…";
  }
}

addEventListener("keydown",e=>{
  if(e.key.toLowerCase()==="b") setMode("BRAIN");
  if(e.key.toLowerCase()==="h") setMode("HUMAN");
  if(e.key.toLowerCase()==="r") reset();
  if(mode==="HUMAN"){
    if(e.key==="ArrowUp"||e.key.toLowerCase()==="w") act("FORWARD");
    if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a") act("LEFT");
    if(e.key==="ArrowRight"||e.key.toLowerCase()==="d") act("RIGHT");
  }
});

document.querySelector("#toggle").onclick=()=>setMode(mode==="HUMAN"?"BRAIN":"HUMAN");
document.querySelector("#reset").onclick=reset;

function resize(){
  const c=renderer.domElement,w=c.clientWidth,h=c.clientHeight;
  if(c.width!==w||c.height!==h){
    renderer.setSize(w,h,false);
    camera.aspect=w/h;
    camera.updateProjectionMatrix();
  }
}

function loop(now){
  resize();
  if(mode==="BRAIN"&&now-brainTimer>120){
    brainStep();
    brainTimer=now;
  }
  document.querySelector("#distance").textContent=distance().toFixed(2);
  renderer.render(scene,camera);
  requestAnimationFrame(loop);
}

reset();
requestAnimationFrame(loop);
