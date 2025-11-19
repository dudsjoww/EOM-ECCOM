export function ConsumablesPicker({
    items,
    onQuantityChange
}: {
    items: { id: number; name: string; price: number }[];
    onQuantityChange: (id: number, qty: number) => void;
}) {
    return (
        <div className="w-full mt-6">
            <h3 className="font-bold mb-3">Consumíveis</h3>

            <div className="flex flex-wrap gap-4">
                {items.map((i) => (
                    <div key={i.id} className="border rounded-xl p-4 w-40 text-center">
                        <h4 className="font-semibold">{i.name}</h4>
                        <p className="text-sm opacity-70">R$ {i.price}</p>

                        <input
                            type="number"
                            min={0}
                            className="mt-2 w-full rounded-lg p-2 border"
                            onChange={(e) => onQuantityChange(i.id, Number(e.target.value))}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}
