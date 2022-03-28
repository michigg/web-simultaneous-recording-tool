import { ref } from 'vue'
import { Ref } from '@vue/reactivity'
import { io, Socket } from 'socket.io-client'

export function useSocketConnection(): {
  socket: Socket
  isConnected: Ref<boolean>
  socketId: Ref<string>
  userCount: Ref<number>
} {
  const isConnected = ref<boolean>(false)
  const socketId = ref<string>('')
  const socketUrl: string = import.meta.env.VITE_SOCKET_URL
  const socket = io(socketUrl, {
    transports: ['polling', 'websocket'],
    upgrade: true,
    reconnection: true,
    reconnectionAttempts: Infinity,
    autoConnect: true,
    rejectUnauthorized: false,
  })

  ref<string>('')
  socket.once('connect', () => {
    console.info(`[SOCKET]: [RECEIVED]: [connect]: ${socket.id}`)
    isConnected.value = true
    socketId.value = socket.id
  })

  socket.on('disconnect', () => {
    console.info('[SOCKET]: [RECEIVED]: [disconnect]')
    isConnected.value = false
    socketId.value = ''
  })

  const userCount = ref<number>(0)
  socket.on('user_count', (count: number) => {
    console.info(`[SOCKET]: [RECEIVED]: [user_count]: UPDATE: ${count}`)
    userCount.value = count
  })

  socket.on('connect_error', (err: Error) => {
    console.error(
      `[SOCKET]: [RECEIVED]: [connect_error]: connect_error due to ${err.message}`
    )
  })

  window.addEventListener('beforeunload', () => {
    socket.close()
  })

  return {
    socket,
    isConnected,
    socketId,
    userCount,
  }
}
