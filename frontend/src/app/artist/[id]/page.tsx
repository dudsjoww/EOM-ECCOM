import ArtistProfile from "@/components/ArtistProfile"

interface ArtistPageProps {
  params: { id: string }
}

export default async function ArtistPage({ params }: ArtistPageProps) {
  const { id } = params

  // Exemplo de mock — depois você vai buscar do backend
  const artist = {
    id,
    name: "Rafael Mendes",
    bio: "I like rock, play games and stuff",
    specialty: "CyberTattoo",
    favoriteTheme: "Metal",
    workShift: "Noturno",
    heroImages: ["/hero1.png", "/hero2.png"],
  }

  return <ArtistProfile artist={artist} />
}
