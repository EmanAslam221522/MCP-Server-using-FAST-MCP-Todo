export const metadata = {
  title: 'Frontend App',
  description: 'Next.js frontend calling Express API',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}