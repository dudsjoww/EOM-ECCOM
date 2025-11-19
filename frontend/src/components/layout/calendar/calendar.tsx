export function Calendar({ onSelect }: { onSelect: (day: number) => void }) {
    const days = Array.from({ length: 30 }, (_, i) => i + 1);

    return (
        <div className="w-full p-4">
            <h3 className="text-lg font-bold mb-3">Calendário</h3>
            <div className="grid grid-cols-7 gap-3 text-center">
                {days.map((d) => (
                    <button
                        key={d}
                        onClick={() => onSelect(d)}
                        className="p-3 rounded-xl bg-gray-100 hover:bg-red-500 hover:text-white transition"
                    >
                        {d}
                    </button>
                ))}
            </div>
        </div>
    );
}
