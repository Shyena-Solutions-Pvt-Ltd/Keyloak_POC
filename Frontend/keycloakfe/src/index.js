import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { AuthProvider } from "react-oidc-context";


const oidcConfig = {
  authority: "http://localhost:8088/auth/realms/drdo_realm",
  client_id: "web_app",
  client_secret: "cPlYucFs8b3wxfWggmfQkg6yUsxLBi4P",
  redirect_uri: window.location.origin + "/resource",
};


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AuthProvider {...oidcConfig}>
    <App />
  </AuthProvider>

);

reportWebVitals();
