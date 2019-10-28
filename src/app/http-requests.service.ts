import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Platform } from '@ionic/angular';
import { Socket } from 'ngx-socket-io';


@Injectable({
  providedIn: 'root'
})
export class HttpRequestsService {

  id: string;
  site = 'http://raspberrypi';
  port = '4000';
  isApp: boolean;
  socketConnected = false;
  frame: any = '';

  constructor(public socket: Socket, private http: HttpClient, platform: Platform) {
    this.isApp = !platform.is('mobileweb') && (document.URL.search('localhost:8100') === -1);

    socket.on('connect', () => {
      this.socketConnected = socket.ioSocket.connected;
    });

    socket.on('disconnect', () => {
      this.socketConnected = socket.ioSocket.connected;
    });

    socket.on('newframe', (obj) => {
      console.log('nuovo frame');
      this.frame = obj.frame;
    });
  }

  socketConnect() {
    return this.socket.connect();
    /*
    return new Promise(resolve => {
        this.socket.connect().then(res => {
          resolve(res);
        }, err =>{
          resolve(err);
        });
    });
    */
  }

  socketSend(name: string, obj: any) {
    this.socket.emit(name, obj);
  }

  socketDisconnect() {
    this.frame = '';
    this.socket.disconnect();
  }

  recordVideo(recordVideo) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.post(this.site + ':' + this.port + '/record', {recordVideo}, {headers, responseType: 'text'});
  }

  getRecordsList() {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.get(this.site + ':' + this.port + '/records', {headers});
  }

  deleteVideo(name) {
    const headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');

    return this.http.post(this.site + ':' + this.port + '/record/delete', {name}, {headers, responseType: 'text'});
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
