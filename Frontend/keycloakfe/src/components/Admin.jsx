import React from 'react'
import { useAuth } from 'react-oidc-context';
import { useSelector } from 'react-redux';

export default function Admin()
{
  const auth = useAuth();

  const { userRoles } = useSelector(state=>state.UserDetails)
  console.log("roles", userRoles)

  if(userRoles.includes("super_admin"))
  {
    return(
      <>
        <div>Admin Dashboard</div>
      </>
    )
  }
  else
  {
    return(
      <>
        <div>you are not a Admin</div>
      </>
    )
  }
}