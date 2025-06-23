#include <QCoreApplication>
#include <csignal>
#include "grpc_server.h"

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    // Set up code that uses the Qt event loop here.
    // Call a.quit() or a.exit() to quit the application.
    // A not very useful example would be including
    // #include <QTimer>
    // near the top of the file and calling
    // QTimer::singleShot(5000, &a, &QCoreApplication::quit);
    // which quits the application after 5 seconds.

    // If you do not need a running Qt event loop, remove the call
    // to a.exec() or use the Non-Qt Plain C++ Application template.

    GrpcServer server("0.0.0.0:50051");
    if (!server.start()) return 1;

    QObject::connect(&app, &QCoreApplication::aboutToQuit, &server, &GrpcServer::stop);

    // Allow Ctrl‑C to quit cleanly
    std::signal(SIGINT, +[](int){ QCoreApplication::quit(); });

    return app.exec();
}
