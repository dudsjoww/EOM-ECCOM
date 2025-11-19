import { Button } from "@/components/ui/button"

export default function Hero() {
  return (
    <section className="bg-gradient-to-b from-gray-200 to-gray-100 text-center py-24">
      <h1 className="text-5xl font-bold mb-4">Bem-vindo ao Studio Tattoo</h1>
      <p className="text-gray-600 mb-8">Arte, precisão e estilo em cada traço.</p>
      <Button className="bg-gray-800 text-white hover:bg-gray-900 rounded-full px-6 py-3">
        Cadastre-se
      </Button>
    </section>
  )
}
