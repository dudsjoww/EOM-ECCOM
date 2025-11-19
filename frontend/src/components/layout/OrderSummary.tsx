export function OrderSummary({
    tattooStyle,
    day,
    time,
    consumables,
    onConfirm
}: {
    tattooStyle: string;
    day: number;
    time: string;
    consumables: { name: string; qty: number; price: number }[];
    onConfirm: () => void;
}) {
    const total = consumables.reduce(
        (acc, c) => acc + c.qty * c.price,
        0
    );

    return (
        <div className="w-full mt-8 p-6 border rounded-xl bg-gray-50 space-y-4">
            <h3 className="text-xl font-bold">Resumo</h3>

            <p><strong>Estilo:</strong> {tattooStyle}</p>
            <p><strong>Dia:</strong> {day}</p>
            <p><strong>Horário:</strong> {time}</p>

            <h4 className="font-semibold mt-4">Consumíveis:</h4>
            <ul className="pl-4 list-disc">
                {consumables.map((c) =>
                    c.qty > 0 ? (
                        <li key={c.name}>
                            {c.qty}× {c.name} — R$ {(c.qty * c.price).toFixed(2)}
                        </li>
                    ) : null
                )}
            </ul>

            <h3 className="text-lg font-bold mt-4">Total estimado: R$ {total.toFixed(2)}</h3>

            <button
                onClick={onConfirm}
                className="w-full py-3 bg-black text-white rounded-xl font-bold hover:bg-red-600 transition"
            >
                Confirmar Solicitação
            </button>
        </div>
    );
}
