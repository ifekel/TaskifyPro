import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    constructor(private http: HttpClient) { }

    signup(userData: any) {
        return this.http.post('http://localhost:8000/api/v1/auth/signup/', userData);

    }

    login(credentials: { email: string, password: string }) {
        return this.http.post('http://localhost:8000/api/v1/auth/signup/', credentials);
    }

    logout() {
        return this.http.get('http://localhost:8000/api/v1/auth/logout/');
    }

    checkIfAuthenticated() {
        return this.http.get('http://localhost:8000/api/v1/auth/status/');
    }
}