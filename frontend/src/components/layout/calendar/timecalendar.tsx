export function TimeCalendar({ times, onPick }: {
    times: string[];
    onPick: (t: string) => void;
}) {
    return (
        <div className="w-full mt-6">
            <h3 className="text-lg font-bold mb-2">Selecione o horário</h3>

            <div className="grid grid-cols-4 gap-3">
                {times.map((t) => (
                    <button
                        key={t}
                        onClick={() => onPick(t)}
                        className="p-2 bg-gray-200 rounded-xl hover:bg-black hover:text-white transition"
                    >
                        {t}
                    </button>
                ))}
            </div>
        </div>
    );
}
