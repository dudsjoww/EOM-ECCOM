export function TattooStyleSelector({
    styles,
    onPick
}: {
    styles: string[];
    onPick: (style: string) => void;
}) {
    return (
        <div className="w-full py-4 flex flex-wrap gap-3 justify-center">
            {styles.map((style) => (
                <button
                    key={style}
                    onClick={() => onPick(style)}
                    className="px-4 py-2 bg-gray-200 rounded-xl hover:bg-gray-300 transition"
                >
                    {style}
                </button>
            ))}
        </div>
    );
}
