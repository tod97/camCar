import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Platform } from '@ionic/angular';
import { Socket } from 'ngx-socket-io';


@Injectable({
  providedIn: 'root'
})
export class HttpRequestsService {

  id: string;
  site = 'http://192.168.1.197';
  port = '5000';
  isApp: boolean;
  socketConnected = false;

  constructor(private socket: Socket, private http: HttpClient, platform: Platform) {
    this.isApp = !platform.is('mobileweb') && (document.URL.search('localhost:8100') === -1);

    socket.on('connect', () => {
      this.socketConnected = socket.ioSocket.connected;
    });

    socket.on('disconnect', () => {
      this.socketConnected = socket.ioSocket.connected;
    });
  }

  socketConnect() {
    this.socket.connect();
  }

  socketSend(name: string, obj: any) {
    this.socket.emit(name, obj);
  }

  socketDisconnect() {
    this.socket.disconnect();
  }

  /*
  apiConnect() {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    this.http.post(this.site + ':' + this.port + '/connect', {
      id: 100
    }, {headers})
    .subscribe(data => {
      console.log('LOG: ' + JSON.stringify(data));
    });
  }

  apiMove(position) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    this.http.post(this.site + ':' + this.port + '/move', {
      id: 100,
      position
    }, {headers})
    .subscribe(data => {
      console.log('LOG: ' + JSON.stringify(data));
    });
  }
  */
}
