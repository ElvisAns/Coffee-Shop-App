import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.page.html',
  styleUrls: ['./user-page.page.scss'],
})
export class UserPagePage implements OnInit {
  loginURL: string;
  userName: String;
  userEmail: String;
  userAvatar: String;
  showLoader = true;

  constructor(public auth: AuthService, private http: HttpClient) {
    this.loginURL = auth.build_login_link('/tabs/user-page');
  }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization', `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  ngOnInit() {
    if (this.auth.activeJWT()) {
      this.http.get(`https://${this.auth.url}/userinfo`, this.getHeaders())
        .subscribe((res: any) => {
          this.userName = res.nickname;
          this.userEmail = res.name;
          this.userAvatar = res.picture;
          setTimeout(()=>{this.showLoader = false},1000);
        })
    }
  }


}
