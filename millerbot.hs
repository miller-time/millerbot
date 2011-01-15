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
import System.Exit
import Text.Printf
import Data.List

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
-- 1)pongs when ping is received, so as to stay connected
-- 2)clean removes leading ':' and everything up to the next ':'
-- 3)eval handles bot commands
listen :: Handle -> IO ()
listen h = forever $ do
  t <- hgetLine h
  let s = init t
  if ping s then pong s else eval h (clean s)
  putStrLn s
 where
  forever a = a >> forever a
  
  clean     = drop 1 . dropWhile (/= ':') . drop 1
  
  ping x    = "PING :" `isPrefixOf` x
  pong x    = write h "PONG" (':' : drop 6 x)

-- eval function:
-- List of available commands.
eval :: Handle -> String -> IO ()
eval h     "!quit"                = write h "QUIT" ":Exiting" >> exitWith ExitSuccess
eval h x | "!echo" `isPrefixOf` x = privmsg h (drop 4 x)
eval _   _                        = return ()  -- ignore everything else

-- privmsg function:
-- wrapper for write, particularly for doing privmsg command
privmsg :: Handle -> String -> IO ()
privmsg h s = write h "PRIVMSG" (chan ++ " :" ++ s)