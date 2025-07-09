import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 10,           // 10 virtual users
  duration: '5m',    // Run for 5 minutes
};

export default function () {
  http.get('http://20.253.196.6:8881/api/json');
  sleep(1);  // Wait 1 second between requests
}

