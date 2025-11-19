import Link from "next/link"

const artists = [
  { id: "1" ,name: "Artist 1", img: "/artists/artist1.png" },
  { id: "2" ,name: "Artist 2", img: "/artists/artist2.png" },
  { id: "3" ,name: "Artist 3", img: "/artists/artist3.png" },
]

export default function Artists() {
  return (
    <section className="bg-white py-16 text-center" id="sectionArtist" >
      <h2 className="text-3xl font-bold mb-12">Tattoo Artists</h2>
      <div className="flex justify-center gap-10">
        {artists.map((a) => (
          <div key={a.name} className="flex flex-col items-center">
            <Link href={`/artist/${a.id}`}>
                <div className="bg-red-500 w-28 h-40 rounded-3xl flex items-center justify-center text-white text-6xl cursor-pointer hover:scale-105 transition">
                  👤
                </div>
              <p className="mt-4">{a.name}</p>
            </Link>
          </div>
        ))}
      </div>
    </section>
  )
}
