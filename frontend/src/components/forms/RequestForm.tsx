// src/components/forms/RequestForm.tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

export function RequestForm({ readOnly = false }: { readOnly?: boolean }) {
  return (
    <form className="flex flex-col gap-4 bg-zinc-800 p-6 rounded-xl">
      <Input label="Cliente" placeholder="Nome do cliente" disabled={readOnly} />
      <Input label="Data" type="date" disabled={readOnly} />
      <Textarea label="Descrição" placeholder="Detalhes da tatuagem" disabled={readOnly} />
      {!readOnly && <Button className="bg-red-600 hover:bg-red-700">Enviar Solicitação</Button>}
    </form>
  )
}
