"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import * as THREE from "three";
import { ArmModel } from "../tattoo/ArmModel";

export function ThreeTattoo({ imageURL }: { imageURL: string | null }) {

    return (
        <div className="w-full h-[500px] bg-black rounded-xl overflow-hidden">
            <Canvas camera={{ position: [0, 1.5, 4], fov: 45 }}>
                <ambientLight intensity={0.6} />
                <directionalLight position={[5, 5, 5]} intensity={1} />

                <ArmModel />

                {imageURL && <TattooPlane imageURL={imageURL} />}

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

function TattooPlane({ imageURL }: { imageURL: string }) {
    const texture = useLoader(THREE.TextureLoader, imageURL);

    return (
        <mesh position={[0.6, 0.5, 0.4]} rotation={[0, -Math.PI / 2, 0]}>
            <planeGeometry args={[0.8, 0.8]} />
            <meshStandardMaterial
                map={texture}
                transparent
                opacity={0.8}
            />
        </mesh>
    );
}
