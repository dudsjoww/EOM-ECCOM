export function ArtistPicker({ artists, onSelect }: {
    artists: { id: number; name: string; avatar: string }[];
    onSelect: (id: number) => void;
}) {
    return (
        <div className="w-full flex justify-center gap-6 py-6">
            {artists.map((artist) => (
                <button
                    key={artist.id}
                    onClick={() => onSelect(artist.id)}
                    className="flex flex-col items-center hover:scale-105 transition"
                >
                    <img
                        src={artist.avatar}
                        className="w-20 h-20 rounded-full object-cover border-2 border-red-500"
                    />
                    <span className="mt-2 text-center font-medium">{artist.name}</span>
                </button>
            ))}
        </div>
    );
}
