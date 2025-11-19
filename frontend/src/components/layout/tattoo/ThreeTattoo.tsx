"use client";

import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import { ArmModel } from "./ArmModel";

export function ThreeTattoo() {
    return (
        <div className="w-full h-[500px] bg-black rounded-xl overflow-hidden">
            <Canvas
                camera={{ position: [0, 1.5, 4], fov: 45 }} // zoom out
            >
                {/* Luzes */}
                <ambientLight intensity={0.6} />
                <directionalLight position={[5, 5, 5]} intensity={1} />
                <directionalLight position={[-5, -5, -5]} intensity={0.6} />

                {/* Plano de fundo circular */}
                <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.3, 0]}>
                    <circleGeometry args={[3, 64]} />
                    <meshStandardMaterial color="#222" />
                </mesh>

                {/* Modelo do braço */}
                <ArmModel />

                {/* Controles */}
                <OrbitControls enablePan={false} enableZoom={true} />

                {/* Ambiente */}
                <Environment preset="studio" />
            </Canvas>
        </div>
    );
}
