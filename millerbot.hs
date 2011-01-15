-- MillerBot
-- Haskell IRC Bot for no particular reason..
--
-- Author: Russell Miller
-- Start date: Jan 2011
-- GNU General Public License
-- http://www.gnu.org/licenses/gpl.html
--


import Network
import System.IO
import Text.Printf

server = "irc.kittenz.pdx.edu"
port   = 6667
chan   = "#kittenz"
nick   = "millerbot"

-- main function:
-- connect to the server, then set the buffering on the socket off. 
-- send messages back to the IRC server using write
main = do
  h <- connectTo server (PortNumber (fromIntegral port))
  hSetBuffering h NoBuffering
  write h "NICK" nick
  write h "USER" (nick++": a useless bot")
  write h "JOIN" chan
  listen h

-- write function:
-- Input: handle(socket), two IRC commands, arguments
-- Uses hPrintf to build an IRC message and write it over the wire to the server. 
-- For debugging purposes also prints the message to standard output.
write :: Handle -> String -> String -> IO ()
write h s t = do
  hPrintf h "%s %s\r\n" s t
  printf    "> %s %s\n" s t

-- listen function:
-- Input: handle
-- In an infinite loop, read lines of text from the network and print them
listen :: Handle -> IO ()
listen h = forever $ do
  s <- hGetLine h
  putStrLn s
 where
  forever a = do a; forever a