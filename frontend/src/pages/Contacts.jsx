import { useEffect, useState } from 'react'
import api from '../api'

export default function Contacts() {
  const [contacts, setContacts] = useState([])
  const [form, setForm] = useState({ name: '', email: '', phone: '', company: '' })
  const [showForm, setShowForm] = useState(false)

  const load = () => api.get('/contacts/').then(r => setContacts(r.data))
  useEffect(() => { load() }, [])

  const create = async e => {
    e.preventDefault()
    await api.post('/contacts/', form)
    setForm({ name: '', email: '', phone: '', company: '' })
    setShowForm(false)
    load()
  }

  const remove = async id => {
    await api.delete(`/contacts/${id}`)
    setContacts(prev => prev.filter(c => c.id !== id))
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">Contacts</h2>
        <button onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700">
          + Add contact
        </button>
      </div>

      {showForm && (
        <form onSubmit={create} className="bg-white border border-gray-200 rounded-xl p-5 mb-6 grid grid-cols-2 gap-3">
          {[['name', 'Name *'], ['email', 'Email'], ['phone', 'Phone'], ['company', 'Company']].map(([field, label]) => (
            <input key={field} placeholder={label} value={form[field]}
              onChange={e => setForm({ ...form, [field]: e.target.value })}
              required={field === 'name'}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
          ))}
          <button type="submit"
            className="col-span-2 bg-indigo-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-indigo-700">Save contact</button>
        </form>
      )}

      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              {['Name', 'Company', 'Email', 'Phone', ''].map(h => (
                <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {contacts.length === 0 && (
              <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-400">No contacts yet</td></tr>
            )}
            {contacts.map(c => (
              <tr key={c.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-800">{c.name}</td>
                <td className="px-4 py-3 text-gray-500">{c.company || '—'}</td>
                <td className="px-4 py-3 text-gray-500">{c.email || '—'}</td>
                <td className="px-4 py-3 text-gray-500">{c.phone || '—'}</td>
                <td className="px-4 py-3 text-right">
                  <button onClick={() => remove(c.id)} className="text-gray-300 hover:text-red-400 text-xs transition-colors">Remove</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
