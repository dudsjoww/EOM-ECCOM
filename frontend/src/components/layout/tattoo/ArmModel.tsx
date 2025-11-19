"use client";

import { useLoader } from "@react-three/fiber";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
import * as THREE from "three";

type ArmModelProps = {
    scale?: number | [number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
};

export function ArmModel({
    scale = 0.02,
    position = [0, 0, 0],
    rotation = [5, 19, 4],
}: ArmModelProps) {

    const obj = useLoader(OBJLoader, "/models/arm.obj");

    return (
        <primitive
            object={obj}
            scale={scale}
            position={position}
            rotation={rotation}
        />
    );
}
