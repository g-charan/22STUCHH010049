import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div>
      Working on the code<Link href={"/urlshortener"}>Go to the shortener</Link>
    </div>
  );
}
