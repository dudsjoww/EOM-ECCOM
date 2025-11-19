import { Check, Zap, Shield } from "lucide-react"

export default function Features() {
  const features = [
    { icon: Check, text: "Simplicidade" },
    { icon: Shield, text: "Foco em Qualidade" },
    { icon: Zap, text: "Rapidez" },
  ]

  return (
    <section className="bg-gray-100 py-12 flex justify-center gap-12">
      {features.map(({ icon: Icon, text }) => (
        <div key={text} className="text-center">
          <Icon className="mx-auto text-3xl mb-2" />
          <p>{text}</p>
        </div>
      ))}
    </section>
  )
}
