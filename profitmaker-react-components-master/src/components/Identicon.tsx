import { useEffect, useRef } from "react";
import Jazzicon from "@suenot/jazzicon";
import styled from "@emotion/styled";

const StyledIdenticon = styled.div<{ size: number }>`
  height: ${(props) => props.size}px;
  width: ${(props) => props.size}px;
  border-radius: 50% !important;
  background-color: black;
  &>div {
    border-radius: 50% !important;
  }
`;

export default function Identicon({ linkId, size }: { linkId: number, size: number }) {
  const ref = useRef<HTMLDivElement>();

  useEffect(() => {
    if (linkId && ref.current) {
      ref.current.innerHTML = "";
      ref.current.appendChild(Jazzicon(size, linkId));
    }
  }, [linkId]);

  return <StyledIdenticon ref={ref as any} size={size} />;
}
