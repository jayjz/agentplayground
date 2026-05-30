export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">AgentPlayground</h1>
      <p className="mt-4 text-gray-600">
        Agentic hedge-fund research copilot
      </p>
      <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Signals</h2>
          <p className="text-sm text-gray-600">Research signals and hypotheses</p>
        </div>
        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Portfolio</h2>
          <p className="text-sm text-gray-600">Paper trading portfolio</p>
        </div>
        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Agents</h2>
          <p className="text-sm text-gray-600">Active research agents</p>
        </div>
      </div>
    </main>
  )
}
