// "use client";

// import { Canvas, useLoader } from "@react-three/fiber";
// import { Environment } from "@react-three/drei";
// import { OrbitControls } from "@react-three/drei";
// import { ArmModel } from "../tattoo/ArmModel";
// import * as THREE from "three";
// import { DecalController } from "../tattoo/DecalController";
// import { useState } from "react";

// export function CanvasTattoo({ imageURL }: { imageURL: string | null }) {
//     const [armMesh, setArmMesh] = useState<THREE.Mesh | null>(null);

//     const [scale, setScale] = useState(0.6); const [rotation, setRotation] = useState(0);

//     return (
//         <Canvas camera={{ position: [0, 1.8, 6], fov: 45 }}>
//             <ambientLight intensity={0.6} />
//             <directionalLight position={[5, 5, 5]} intensity={1} />

//             <ArmModel onMeshReady={setArmMesh} />

//             {armMesh && imageURL && (
//                 <DecalController armMesh={armMesh} imageURL={imageURL} />
//             )}

//             <OrbitControls
//                 enablePan={false}
//                 enableZoom={true}
//                 minDistance={2}
//                 maxDistance={8}
//                 zoomSpeed={0.6}
//             />

//             <Environment preset="studio" />
//         </Canvas>
//     );
// }

