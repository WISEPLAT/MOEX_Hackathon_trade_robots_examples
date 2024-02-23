import * as React from "react"
import Identicon from "./Identicon";

import {
  Box,
  Avatar,
} from "@chakra-ui/react"

export const AvatarUi = ({src, id, size}: {src: string, id: number, size: number}) => {
  return (
    <Box>
      {src ? (<Avatar size={`${size}px`} name='' src={src} mb='1' />) : (<Identicon linkId={id} size={size} />)}
    </Box>
  )
}
