
export const mqttEnv = {
    server: 'broker.mqttdashboard.com',
    protocol: "ws",
    port: 8000,
    clean: true,
    clientId: (Math.random()*10000000).toFixed(0)+'',
    path: '/mqtt',
    connectTimeout: 4000, // Timeout period
    reconnectPeriod: 4000 // Reconnect period

  };


 