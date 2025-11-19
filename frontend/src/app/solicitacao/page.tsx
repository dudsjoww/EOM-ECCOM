"use client";

import { useState } from "react";

import Header from "@/components/layout/header"
import { ArtistPicker } from "@/components/layout/ArtistPicker";
import { ThreeTattoo } from "@/components/layout/threeUploader/ThreeUploader";
import { TattooStyleSelector } from "@/components/layout/TattooStyleSelector";
import { Calendar } from "@/components/layout/calendar/calendar";
import { TimeCalendar } from "@/components/layout/calendar/timecalendar";
import { ConsumablesPicker } from "@/components/layout/consumables/ConsumablesPicker";
import { OrderSummary } from "@/components/OrderSummary";

export default function SolicitacaoPage() {

    const [artistId, setArtistId] = useState<number | null>(null);
    const [selectedStyle, setSelectedStyle] = useState<string>("");
    const [selectedDay, setSelectedDay] = useState<number | null>(null);
    const [selectedTime, setSelectedTime] = useState<string>("");

    // === ESTADO DA IMAGEM ===
    const [imageURL, setImageURL] = useState<string | null>(null);

    // === UPLOAD DA IMAGEM ===
    const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        setImageURL(url);
    };

    const [consumables, setConsumables] = useState([
        { id: 1, name: "Tinta", price: 25, qty: 0 },
        { id: 2, name: "Agulha", price: 12, qty: 0 },
        { id: 3, name: "Grip", price: 40, qty: 0 },
        { id: 4, name: "Luvas", price: 8, qty: 0 },
    ]);

    const handleConsumableQty = (id: number, qty: number) => {
        setConsumables((prev) =>
            prev.map((c) => (c.id === id ? { ...c, qty } : c))
        );
    };

    const handleConfirm = () => {
        const resumo = {
            tatuador: artistId,
            estilo: selectedStyle,
            dia: selectedDay,
            horario: selectedTime,
            imagem: imageURL,
            consumiveis: consumables.filter((c) => c.qty > 0),
        };

        console.log("🎉 Solicitação enviada:", resumo);

        alert("Solicitação registrada! Depois conectamos ao backend.");
    };

    const artists = [
        { id: 1, name: "Artist 1", avatar: "https://i.pravatar.cc/150?img=1" },
        { id: 2, name: "Artist 2", avatar: "https://i.pravatar.cc/150?img=2" },
        { id: 3, name: "Artist 3", avatar: "https://i.pravatar.cc/150?img=3" },
    ];

    const tattooStyles = ["Realismo", "Blackwork", "Oldschool", "Minimalista"];

    const horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"];


    return (
        <div className="min-h-screen bg-gray-100 pb-24">
            <Header />

            <main className="max-w-3xl mx-auto mt-8 p-4 flex flex-col gap-10">

                {/* UPLOAD */}
                <section className="flex flex-col gap-2">
                    <label className="font-bold">Enviar referência da tattoo:</label>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleUpload}
                        className="bg-white p-2 rounded shadow"
                    />
                </section>

                {/* PREVIEW 3D */}
                <section>
                    <ThreeTattoo imageURL={imageURL} />
                </section>

                {/* TATUADOR */}
                <section>
                    <h2 className="text-center text-xl font-bold mb-4">
                        Se preferir, escolha o tatuador:
                    </h2>
                    <ArtistPicker artists={artists} onSelect={setArtistId} />
                </section>

                {/* ESTILO */}
                <section>
                    <h2 className="text-lg font-bold mb-2">Estilos disponíveis</h2>
                    <TattooStyleSelector
                        styles={tattooStyles}
                        onPick={setSelectedStyle}
                    />
                </section>

                {/* CALENDÁRIO */}
                <section>
                    <Calendar onSelect={setSelectedDay} />
                </section>

                {/* HORÁRIO */}
                <section>
                    <TimeCalendar times={horarios} onPick={setSelectedTime} />
                </section>

                {/* CONSUMÍVEIS */}
                <section>
                    <ConsumablesPicker
                        items={consumables}
                        onQuantityChange={handleConsumableQty}
                    />
                </section>

                {/* RESUMO */}
                {selectedStyle && selectedDay && selectedTime && (
                    <section>
                        <OrderSummary
                            tattooStyle={selectedStyle}
                            day={selectedDay}
                            time={selectedTime}
                            consumables={consumables}
                            onConfirm={handleConfirm}
                        />
                    </section>
                )}
            </main>
        </div>
    );
}
