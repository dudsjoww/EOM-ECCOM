"use client";

import { Decal, useTexture } from "@react-three/drei";

export function TattooDecal({ imageURL }: { imageURL: string }) {
    const decalTexture = useTexture(imageURL);

    return (
        <Decal
            position={[0.2, 0.1, 0.3]} // onde na superfície
            rotation={[0, 0, 0]}       // rotação da tattoo
            scale={[0.4, 0.4, 0.4]}    // tamanho da tattoo
        >
            <meshStandardMaterial
                map={decalTexture}
                transparent
                polygonOffset
                polygonOffsetFactor={-1}
                depthWrite={false}
            />
        </Decal>
    );
}
