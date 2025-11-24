"use client";

import { useEffect } from "react";
import { useLoader } from "@react-three/fiber";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
import { FBXLoader } from "three/examples/jsm/loaders/FBXLoader.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as THREE from "three";

type ArmModelProps = {
    scale?: number | [number, number, number];
    position?: [number, number, number];
    rotation?: [number, number, number];
    onMeshReady?: (mesh: THREE.Mesh) => void;
};

export function ArmModel({
    // scale = 0.02,
    // position = [0, 0, 0],
    // rotation = [5, 19, 4],
    scale = 1,
    position = [7, -10, -15],
    rotation = [0, 0, 0],
    onMeshReady,
}: ArmModelProps) {
    // const obj = useLoader(OBJLoader, "/models/arm.obj");
    // const obj = useLoader(FBXLoader, "/models/arm.fbx");
    const obj = useLoader(GLTFLoader, "/models/lowpoly_arm/arm.gltf");

    useEffect(() => {
        if (!obj) return;

        // Pega o primeiro mesh encontrado no OBJ
        // const mesh = obj.getObjectByProperty("type", "Mesh") as THREE.Mesh;

        const mesh = (obj as any).scene?.getObjectByProperty("type", "Mesh");

        if (mesh && onMeshReady) {
            onMeshReady(mesh);
        }
    }, [obj, onMeshReady]);

    return (
        <primitive
            object={obj.scene || obj}
            scale={scale}
            position={position}
            rotation={rotation}
        />
    );


}
