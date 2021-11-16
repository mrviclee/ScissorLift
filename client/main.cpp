#include <cstring>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

std::vector<std::string> split(std::string s, std::string sep, int num) {
    std::vector<std::string> rvalue;
    if (sep == "") {
        rvalue.push_back(s);
        return rvalue;
    }

    int start = 0;
    int end = s.find(sep);
    int count = 1;
    while (end != -1) {
        if (num != -1 && count >= num) {
            end = s.size();
            break;
        }
        rvalue.push_back(s.substr(start, end - start));
        start = end + sep.size();
        end = s.find(sep, start);
        count += 1;
    }
    rvalue.push_back(s.substr(start, end - start));

    return rvalue;
}

std::string listen(int socket){
    std::vector<std::string> arr;
    std::string reply(1024, 0);
    while (true) {

        // recv() call tries to get the response from server
        // BUT there's a catch here, the response might take multiple calls
        // to recv() before it is completely received
        // will be demonstrated in another example to keep this minimal
        auto bytes_recv = recv(socket, &reply.front(), reply.size(), 0);
        if (bytes_recv == -1) {
            std::cerr << "Error while receiving bytes\n";
            return "-6";
        }

        arr = split(reply, ":", 2);
        if (arr.size() < 2) {
            std::cerr << "Invalid message from server: " << reply << std::endl;
            continue;
        }

        if (arr.at(0) == "msg"){
            std::string rvalue = arr.at(1);
            rvalue.erase(std::find(rvalue.begin(), rvalue.end(), '\0'), rvalue.end());
            return rvalue;
        }
    }
}

void log_error(std::string msg="") {
    std::cerr << "ERROR: " << msg << std::endl;
}

void log_message(std::string msg="") {
    std::cout << "MESSAGE: " << msg;
}

std::string run_cmd(int sock, std::string cmd, bool failOnError=true, bool logError = true) {
    std::string msg = cmd;
    msg = cmd + "\n";
    write(sock, cmd.c_str(), cmd.size());
    msg = listen(sock);
    if (msg != "True") {
        if (logError)
            log_error("Failed running command \"" + cmd + "\" error code: " + msg);
        if (failOnError){
            if(cmd == "is_level")exit(1);
            if(cmd == "open")exit(2);
            if(cmd == "is_open")exit(3);
            if(cmd == "lift:1000")exit(4);
            if(cmd == "lower:1000")exit(5);
        }
    }
    return msg;
}

std::string move(int sock, std::string cmd, std::string timeout) {
    bool failOnFailure = false;
    std::string ret = "timeout";
    printf("Running %s", cmd.c_str());
    int iTimeout = 0;
    std::string interval = "1000";
    while(ret == "timeout" && iTimeout < std::atoi(timeout.c_str())){
        ret = run_cmd(sock, cmd + ":" + interval, failOnFailure, false);
        printf(".");
        fflush(stdout);
        iTimeout += std::atoi(interval.c_str());
    }
    printf("\n");
    fflush(stdout);
    return ret;
}

void open_proc(int sock) {
    std::vector<std::string> arr;
    std::string reply(1024, 0);

    std::string ret;
    run_cmd(sock, "is_level");
    
    ret = run_cmd(sock, "is_open", false);
    if (ret != "True")
        run_cmd(sock, "open");
    run_cmd(sock, "is_open");
    
    move(sock, "lift", "150000");
    
}

void close_proc(int sock) {
    move(sock, "lower", "150000");
}

int main(int argc, char *argv[])
{
    // Now we're taking an ipaddress and a port number as arguments to our program
    char ipAddress[] = "raspberrypi";
    char portNum[]  = "6000";

    addrinfo hints, *p;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family   = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags    = AI_PASSIVE;

    int gAddRes = getaddrinfo(ipAddress, portNum, &hints, &p);
    if (gAddRes != 0) {
        std::cerr << gai_strerror(gAddRes) << "\n";
        return -2;
    }

    if (p == NULL) {
        std::cerr << "No addresses found\n";
        return -3;
    }

    // socket() call creates a new socket and returns it's descriptor
    int sockFD = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
    if (sockFD == -1) {
        std::cerr << "Error while creating socket\n";
        return -4;
    }

    // Note: there is no bind() call as there was in Hello TCP Server
    // why? well you could call it though it's not necessary
    // because client doesn't necessarily has to have a fixed port number
    // so next call will bind it to a random available port number

    // connect() call tries to establish a TCP connection to the specified server
    int connectR = connect(sockFD, p->ai_addr, p->ai_addrlen);
    if (connectR == -1) {
        close(sockFD);
        std::cerr << "Error while connecting socket\n";
        return -5;
    }

    std::string in = "";
    char value;
    while (in != "q") {
        std::cout << "Press \"O\" to open and \"C\" to close.  Press \"q\" to quit." << std::endl;
        std::cin >> in;
        value = in.at(0);
        value = tolower(value);
        if (value == 'o') {
            std::cout << "Starting open process." << std::endl;
            open_proc(sockFD);
        } else if (value == 'c') {
            std::cout << "Starting close process." << std::endl;
            close_proc(sockFD);
        }
    }
    close(sockFD);
    freeaddrinfo(p);

    return 0;
}
