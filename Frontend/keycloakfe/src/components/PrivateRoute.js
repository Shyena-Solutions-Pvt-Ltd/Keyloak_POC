import { useAuth } from "react-oidc-context";
import { Outlet } from "react-router-dom";
import React from "react";



const PrivateRoute = () => {
 const auth = useAuth();

 const isLoggedIn = auth.isAuthenticated;

 return isLoggedIn ? <Outlet/> : null;
};

export default PrivateRoute;