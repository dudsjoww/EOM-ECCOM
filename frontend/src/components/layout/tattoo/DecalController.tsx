import { DecalGeometry } from "three/examples/jsm/geometries/DecalGeometry.js";
import { useEffect, useRef } from "react";
import { useThree, useLoader } from "@react-three/fiber";
import * as THREE from "three";

import { MeshBVH, acceleratedRaycast } from "three-mesh-bvh";

THREE.Mesh.prototype.raycast = acceleratedRaycast;

export function DecalController({
    armMesh,
    imageURL,
    scale,
    rotation,
}: {
    armMesh: THREE.Mesh;
    imageURL: string;
    scale: number;
    rotation: number;
}) {
    const scene = useThree((state) => state.scene);
    const camera = useThree((state) => state.camera);

    const texture = useLoader(THREE.TextureLoader, imageURL);
    const raycaster = new THREE.Raycaster();
    raycaster.firstHitOnly = true;

    const mouse = new THREE.Vector2();
    const decalRef = useRef<THREE.Mesh | null>(null);
    const initialized = useRef(false);

    // ==========================================================
    // 📌 PREPARAÇÃO DA MALHA (BVH)
    // ==========================================================
    useEffect(() => {
        if (!armMesh || initialized.current) return;

        // obrigatórios
        armMesh.geometry.computeBoundingBox();
        armMesh.geometry.computeBoundingSphere();

        // cria BVH na API nova
        armMesh.geometry.boundsTree = new MeshBVH(armMesh.geometry);

        initialized.current = true;
    }, [armMesh]);

    // ==========================================================
    // 📌 APLICAÇÃO DO DECAL
    // ==========================================================
    useEffect(() => {
        if (!armMesh) return;

        function handleClick(e: MouseEvent) {
            const rect = (e.target as HTMLElement).getBoundingClientRect();

            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);

            const hit = raycaster.intersectObject(armMesh, true)[0];

            if (!hit) {
                console.warn("❌ Nenhum hit detectado.");
                return;
            }

            const position = hit.point.clone();
            const normal = hit.face!.normal.clone();

            // Corrige normal local → world space
            normal.transformDirection(armMesh.matrixWorld).normalize();

            // Prevê decal invertido
            const camDir = camera.getWorldDirection(new THREE.Vector3());
            if (normal.dot(camDir) > 0) normal.multiplyScalar(-1);

            const orientation = new THREE.Euler();
            orientation.setFromQuaternion(
                new THREE.Quaternion().setFromUnitVectors(
                    new THREE.Vector3(0, 0, 1),
                    normal
                )
            );

            const size = new THREE.Vector3(scale, scale, scale * 0.35);

            const decalGeom = new DecalGeometry(armMesh, position, orientation, size);

            const decalMat = new THREE.MeshStandardMaterial({
                map: texture,
                transparent: true,
                depthTest: true,
                depthWrite: false,
                polygonOffset: true,
                polygonOffsetFactor: -4,
                polygonOffsetUnits: -4,
            });

            if (decalRef.current) scene.remove(decalRef.current);

            const decalMesh = new THREE.Mesh(decalGeom, decalMat);
            decalMesh.renderOrder = 999;

            scene.add(decalMesh);
            decalRef.current = decalMesh;
        }

        window.addEventListener("pointerdown", handleClick);
        return () => window.removeEventListener("pointerdown", handleClick);
    }, [armMesh, texture, scale]);

    // ==========================================================
    // 📌 Atualização dinâmica de escala/rotação
    // ==========================================================
    useEffect(() => {
        if (!decalRef.current) return;
        decalRef.current.scale.set(scale, scale, scale * 0.35);
        decalRef.current.rotation.z = rotation;
    }, [scale, rotation]);

    return null;
}
