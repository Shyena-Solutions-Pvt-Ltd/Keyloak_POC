import React from 'react'
import { useAuth } from 'react-oidc-context';
import { useSelector } from 'react-redux';

export default function RegularUser()
{
  const auth = useAuth();

  const { userRoles } = useSelector(state=>state.UserDetails)
  console.log("roles", userRoles)

  if(userRoles.includes("regular_user"))
  {
    return(
      <>
        <div>Regular User Dashboard</div>
      </>
    )
  }
  else
  {
    return(
      <>
        <div>you are not a Regular User</div>
      </>
    )
  }
}