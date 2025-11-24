import { DecalGeometry } from "three/examples/jsm/geometries/DecalGeometry.js";
import { useEffect, useRef } from "react";
import { useThree, useLoader } from "@react-three/fiber";
import * as THREE from "three";

export function DecalController({
    armMesh,
    imageURL,
    scale,
    rotation,
}: {
    armMesh: THREE.Mesh;
    imageURL: string;
    scale: number;      // vindo do slider
    rotation: number;   // vindo do slider
}) {
    const scene = useThree((state) => state.scene);
    const camera = useThree((state) => state.camera);


    const texture = useLoader(THREE.TextureLoader, imageURL);
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    // Referência ao decal atual
    const decalRef = useRef<THREE.Mesh | null>(null);

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
            const normal = hit.face!.normal.clone().normalize();

            // Orientação correta pela normal
            const orientation = new THREE.Euler();
            orientation.setFromQuaternion(
                new THREE.Quaternion().setFromUnitVectors(
                    new THREE.Vector3(0, 0, 1),
                    normal
                )
            );

            const size = new THREE.Vector3(
                scale,
                scale,
                scale * 0.3
            );

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
                depthWrite: false,
                polygonOffset: true,
                polygonOffsetFactor: -4,
                polygonOffsetUnits: -4,
            });

            // Se existe decal anterior, remove antes
            if (decalRef.current) {
                scene.remove(decalRef.current);
            }

            const decalMesh = new THREE.Mesh(decalGeom, decalMat);
            scene.add(decalMesh);

            decalRef.current = decalMesh;
        }

        window.addEventListener("pointerdown", handleClick);
        return () => window.removeEventListener("pointerdown", handleClick);
    }, [armMesh, texture, scale]);

    // Reaplicar ajustes quando os sliders mudarem
    useEffect(() => {
        if (!decalRef.current) return;

        decalRef.current.scale.set(
            scale,
            scale,
            scale * 0.3
        );

        decalRef.current.rotation.z = rotation;

    }, [scale, rotation]);

    return null;


}
