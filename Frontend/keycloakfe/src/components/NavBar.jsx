import {Link} from 'react-router-dom'
import React from 'react'
import { AuthProvider, useAuth } from "react-oidc-context"
import { useDispatch, useSelector } from 'react-redux';
import { setUserRoles } from '../redux/reducers/UserDetails';
import jwt from "jwt-decode";

export default function NavBar() {
  const auth = useAuth();
  const { userRoles } = useSelector(state => state.UserDetails)
  const dispatch = useDispatch()

  if(auth.isAuthenticated && userRoles && userRoles.length<=0)
  {
    const access_token = auth.user ? auth.user.access_token : ""
    const decoded = jwt(access_token);
    const roles = decoded.realm_access ? decoded.realm_access.roles : []
    dispatch(setUserRoles(roles))
  }

  console.log("Roles ",userRoles)
  return (
    <nav>
      <div className='flex justify-around items-center py-5 bg-[#234] text-white'>
        <h1 className='font-semibold font-2xl'>KeyCloak App</h1>
        <ul className='flex'>

          <li className='mx-1'>
            <Link to='/'>Home</Link>
          </li>
          {
            auth.isAuthenticated
            ?
            <li className='mx-1'>
              <button onClick={()=>auth.removeUser()}>Logout</button>
            </li>
            :
            <li className='mx-1'>
              <button onClick={()=>auth.signinRedirect()}>Login</button>
            </li>
          }
          <li className='mx-1'>
            <Link to ='/resource'>Resource</Link>
          </li>
          <li className='mx-1'>
            <Link to ='/super_admin'>Super Admin</Link>
          </li>
          <li className='mx-1'>
            <Link to ='/admin'>Admin</Link>
          </li>
          <li className='mx-1'>
            <Link to ='/regular_user'>Regular User</Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}