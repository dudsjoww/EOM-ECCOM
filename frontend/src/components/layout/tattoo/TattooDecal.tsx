"use client";

import { DecalGeometry } from "three/examples/jsm/geometries/DecalGeometry.js";
import { useEffect } from "react";
import { useThree, useLoader } from "@react-three/fiber";
import * as THREE from "three";

export function DecalController({ armMesh, imageURL }: { armMesh: THREE.Mesh, imageURL: string }) {
    const scene = useThree((state) => state.scene);
    const camera = useThree((state) => state.camera);

    const texture = useLoader(THREE.TextureLoader, imageURL);
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    useEffect(() => {
        if (!armMesh) return;

        function handleClick(e: MouseEvent) {
            const rect = (e.target as HTMLElement).getBoundingClientRect();

            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const hit = raycaster.intersectObject(armMesh)[0];
            if (!hit) return;

            const position = hit.point.clone();
            const normal = hit.face!.normal.clone();

            // Orientação alinhada com a normal da face
            const orientation = new THREE.Euler().setFromVector3(normal);
            const size = new THREE.Vector3(0.25, 0.25, 0.02);

            const decalGeom = new DecalGeometry(
                armMesh,
                position,
                orientation,
                size
            );

            const decalMat = new THREE.MeshStandardMaterial({
                map: texture,
                transparent: true,
                depthTest: true,
                depthWrite: false
            });

            const decalMesh = new THREE.Mesh(decalGeom, decalMat);
            scene.add(decalMesh);

            // Aqui você já pode salvar a posição para usar depois
            console.log({
                pos: position,
                rot: orientation,
                size: size
            });
        }

        window.addEventListener("pointerdown", handleClick);
        return () => window.removeEventListener("pointerdown", handleClick);
    }, [armMesh, texture]);

    return null;
}
