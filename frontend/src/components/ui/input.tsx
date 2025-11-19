import * as React from "react"
import { cn } from "@/lib/util"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, ...props }, ref) => {
    return (
      <div className="flex flex-col space-y-1 w-full">
        {label && (
          <label className="text-sm font-medium text-gray-200">{label}</label>
        )}
        <input
          type={type}
          className={cn(
            "flex h-10 w-full rounded-md border border-neutral-600 bg-neutral-100/95 px-3 py-2 text-sm text-black placeholder:text-neutral-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-600 focus-visible:ring-offset-2 focus-visible:ring-offset-neutral-900 disabled:cursor-not-allowed disabled:opacity-50",
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <span className="text-xs text-red-400">{error}</span>}
      </div>
    )
  }
)

Input.displayName = "Input"

export { Input }
