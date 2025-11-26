"use client";

import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import * as THREE from "three";
import { DecalController } from "../tattoo/DecalController";
import { useState } from "react";
import { ArmModel } from "../tattoo/ArmModel";

export function ThreeTattoo({ imageURL }: { imageURL: string | null }) {


    const [armMesh, setArmMesh] = useState<THREE.Mesh | null>(null);

    // valores controlados pelos sliders
    const [scale, setScale] = useState(0.6);
    const [rotation, setRotation] = useState(0);

    return (
        <div className="relative w-full h-[500px] bg-black rounded-xl overflow-hidden">

            {/* SLIDERS DE CONTROLE */}
            <div className="absolute top-3 left-3 z-10 text-white">
                <div className="mb-2">
                    <label className="block text-sm mb-1">Tamanho</label>
                    <input
                        type="range"
                        min={0.1}
                        max={2}
                        step={0.01}
                        value={scale}
                        onChange={(e) => setScale(Number(e.target.value))}
                    />
                </div>

                <div>
                    <label className="block text-sm mb-1">Rotação</label>
                    <input
                        type="range"
                        min={-Math.PI}
                        max={Math.PI}
                        step={0.01}
                        value={rotation}
                        onChange={(e) => setRotation(Number(e.target.value))}
                    />
                </div>
            </div>

            {/* CANVAS 3D */}
            <Canvas camera={{ position: [0, 1.5, 4], fov: 45 }}>
                <ambientLight intensity={1} />
                <directionalLight position={[5, 5, 5]} intensity={1} />

                <ArmModel onMeshReady={setArmMesh} />
                {/* TODO: DO UV PROJECTING AND IMPROVE FPS */}
                {armMesh && imageURL && (
                    <DecalController
                        armMesh={armMesh}
                        imageURL={imageURL}
                        rotation={rotation}
                        scale={scale}
                    />
                )}

                {/* Piso para referência visual */}
                <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.3, 0]}>
                    <circleGeometry args={[3, 64]} />
                    <meshStandardMaterial color="#222" />
                </mesh>

                <OrbitControls enablePan={false} enableZoom={true} />
                <Environment preset="studio" />
            </Canvas>
        </div>
    );

}
