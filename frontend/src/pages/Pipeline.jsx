import { useEffect, useState } from 'react'
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'
import api from '../api'

const STAGES = ['new', 'contacted', 'negotiating', 'won', 'lost']
const STAGE_COLORS = {
  new: 'bg-gray-100 text-gray-700',
  contacted: 'bg-blue-50 text-blue-700',
  negotiating: 'bg-amber-50 text-amber-700',
  won: 'bg-green-50 text-green-700',
  lost: 'bg-red-50 text-red-600',
}

export default function Pipeline() {
  const [leads, setLeads] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', value: '', notes: '' })

  const load = () => api.get('/leads/').then(r => setLeads(r.data))
  useEffect(() => { load() }, [])

  const byStage = stage => leads.filter(l => l.stage === stage)

  const onDragEnd = async ({ source, destination, draggableId }) => {
    if (!destination || destination.droppableId === source.droppableId) return
    const newStage = destination.droppableId
    setLeads(prev => prev.map(l => l.id === parseInt(draggableId) ? { ...l, stage: newStage } : l))
    await api.patch(`/leads/${draggableId}`, { stage: newStage })
  }

  const createLead = async e => {
    e.preventDefault()
    await api.post('/leads/', { ...form, value: parseFloat(form.value) || 0 })
    setForm({ title: '', value: '', notes: '' })
    setShowForm(false)
    load()
  }

  const deleteLead = async id => {
    await api.delete(`/leads/${id}`)
    setLeads(prev => prev.filter(l => l.id !== id))
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">Pipeline</h2>
        <button onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
          + Add lead
        </button>
      </div>

      {showForm && (
        <form onSubmit={createLead} className="bg-white border border-gray-200 rounded-xl p-5 mb-6 flex gap-3 flex-wrap">
          <input placeholder="Lead title" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} required
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm flex-1 min-w-40 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
          <input placeholder="Value ($)" type="number" value={form.value} onChange={e => setForm({ ...form, value: e.target.value })}
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm w-32 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
          <input placeholder="Notes" value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })}
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm flex-1 min-w-40 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
          <button type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">Save</button>
        </form>
      )}

      <DragDropContext onDragEnd={onDragEnd}>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {STAGES.map(stage => (
            <div key={stage} className="flex-shrink-0 w-56">
              <div className={`text-xs font-semibold uppercase tracking-wide px-3 py-1.5 rounded-lg mb-3 inline-block ${STAGE_COLORS[stage]}`}>
                {stage} · {byStage(stage).length}
              </div>
              <Droppable droppableId={stage}>
                {(provided, snapshot) => (
                  <div ref={provided.innerRef} {...provided.droppableProps}
                    className={`min-h-32 rounded-xl p-2 transition-colors ${snapshot.isDraggingOver ? 'bg-indigo-50' : 'bg-gray-100'}`}>
                    {byStage(stage).map((lead, index) => (
                      <Draggable key={lead.id} draggableId={String(lead.id)} index={index}>
                        {(provided) => (
                          <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}
                            className="bg-white border border-gray-200 rounded-lg p-3 mb-2 shadow-sm group">
                            <div className="flex justify-between items-start">
                              <p className="text-sm font-medium text-gray-800 leading-snug">{lead.title}</p>
                              <button onClick={() => deleteLead(lead.id)}
                                className="text-gray-300 hover:text-red-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity ml-2">✕</button>
                            </div>
                            {lead.value > 0 && (
                              <p className="text-xs text-indigo-600 font-medium mt-1">${lead.value.toLocaleString()}</p>
                            )}
                            {lead.notes && <p className="text-xs text-gray-400 mt-1 truncate">{lead.notes}</p>}
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  )
}
