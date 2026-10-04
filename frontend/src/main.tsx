import React from 'react'
import ReactDOM from 'react-dom/client'
import './styles.css'

function App() {
  return (
    <main className="min-h-screen bg-ink text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col gap-8 px-6 py-10 lg:px-10">
        <header className="rounded-3xl border border-white/10 bg-gradient-to-br from-slatepanel via-[#10182a] to-[#0b1120] p-8 shadow-panel">
          <p className="text-sm uppercase tracking-[0.35em] text-aurora">Agent Execution Platform</p>
          <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            Orchestrate resilient AI workflows with real state, real queues, and real observability.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
            Phase 1 establishes the backend foundation, relational workflow state, and the UI shell for a production-grade execution system.
          </p>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-panel backdrop-blur">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white">Create workflow</h2>
              <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300">Phase 1 shell</span>
            </div>
            <div className="mt-6 space-y-4">
              <textarea
                className="min-h-40 w-full rounded-2xl border border-white/10 bg-[#0a0f1d] p-4 text-sm text-slate-200 outline-none transition focus:border-aurora/60"
                value={'Research the latest multimodal RAG papers, compare the top 5, summarize their approaches, and produce a report.'}
                readOnly
              />
              <button className="rounded-2xl bg-aurora px-5 py-3 text-sm font-semibold text-slate-950 transition hover:brightness-110">
                Submit plan
              </button>
            </div>
          </div>

          <div className="grid gap-6">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-panel">
              <h2 className="text-xl font-semibold text-white">System status</h2>
              <dl className="mt-4 grid gap-3 text-sm text-slate-300">
                <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                  <dt>API</dt>
                  <dd className="text-signal">online</dd>
                </div>
                <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                  <dt>Database</dt>
                  <dd className="text-warning">provisioned</dd>
                </div>
                <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                  <dt>Queue</dt>
                  <dd className="text-slate-300">planned</dd>
                </div>
              </dl>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-panel">
              <h2 className="text-xl font-semibold text-white">Execution timeline</h2>
              <div className="mt-4 space-y-3 text-sm text-slate-300">
                <p>Workflow created</p>
                <p>Task graph persisted</p>
                <p>Queue integration pending</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
