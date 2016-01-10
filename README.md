Fullstack Nano 2 - Tournament Scheduler
=======================================
_Forked from udacity/fullstack-nanodegree-vm_

Common code for the Relational Databases and Full Stack Fundamentals courses

Setup(Mac):
-----------

1. Install [VirtualBox](https://www.virtualbox.org) and [Vagrant](http://vagrantup.com/)

2. Clone this repository.

  ``` git clone https://github.com/maweeks/nano-fs-02.git ```

3. Open the terminal application

4. Navigate inside the cloned repository, into the vagrant folder.

	``` cd [REPOSITORY_LOCATION]/nano-fs-02/vagrant ````

5. Start up and connect to the vagrant machine using the following command:

  ``` vagrant up; vagrant ssh; '''

6. Set up the database on the VM using the following command:

  ``` cd /vagrant/tournament/; psql -c '\i tournament.sql; \q'; ```

_The database is now set up to be used._

Import tournament.py into python to create tournaments.


Functions to run a tournament (see the example in t-test.py):
-------------------------------------------------------------

1. createTournament(name)

2. registerPlayer(name) and activatePlayer(id)

3. beginTournament()

4. swissPairings()

5. reportMatch(pida, pidb, status)

6. Repeat steps

Additional Features:
--------------------

* Multiple tournaments supported (only one active tournament at a time).

* Tied games are supported.

* When players have the same number of points it is then ranked by the OMP (Opponent Match points)


Current restrictions:
---------------------

* Rematches between players are not avoided.

* Assumes an even number of players.
