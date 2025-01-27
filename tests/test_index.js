import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 10 }, // 10 usuários simultâneos por 30 segundos
        { duration: '1m', target: 50 }, // 50 usuários simultâneos por 1 minuto
        { duration: '10s', target: 0 }, // Reduz para 0 usuários
    ],
};

export default function () {
    let res = http.get('http://127.0.0.1:5000/test_index'); // Altere para o endpoint do Flask
    check(res, {
        'status was 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
    });
    sleep(1);
}
