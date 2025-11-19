"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { Environment } from "@react-three/drei";
import { OrbitControls } from "@react-three/drei";
import { ArmModel } from "../tattoo/ArmModel";
import * as THREE from "three";

export function CanvasTattoo({ imageURL }: { imageURL: string | null }) {
    return (
        <Canvas camera={{ position: [0, 1.8, 6], fov: 45 }}>
            <ambientLight intensity={0.6} />
            <directionalLight position={[5, 5, 5]} intensity={1} />

            <ArmModel />

            {imageURL && <TattooPlane imageURL={imageURL} />}

            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.3, 0]}>
                <circleGeometry args={[3, 64]} />
                <meshStandardMaterial color="#222" />
            </mesh>

            <OrbitControls
                enablePan={false}
                enableZoom={true}
                minDistance={2}
                maxDistance={8}
                zoomSpeed={0.6}
            />

            <Environment preset="studio" />
        </Canvas>

    );
}

function TattooPlane({ imageURL }: { imageURL: string }) {
    const texture = useLoader(THREE.TextureLoader, imageURL);

    return (
        <mesh>
            <planeGeometry args={[2, 2]} />
            <meshBasicMaterial map={texture} toneMapped={false} />
        </mesh>
    );
}
