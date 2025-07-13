import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

function BetTrackerTable() {
    const [bets, setBets] = useState([]);

    useEffect(() => {
        fetchBets();
    }, []);

    const fetchBets = async () => {
        try {
            const response = await fetch('/api/bets');
            const data = await response.json();
            setBets(data);
        } catch (error) {
            console.error("Error fetching bets:", error);
        }
    };

    const handleDeleteBet = async (betId) => {
        try {
            const response = await fetch(`/api/bets/${betId}`, {
                method: 'DELETE',
            });
            if (response.ok) {
                fetchBets(); // Refresh bets after deletion
            } else {
                console.error("Failed to delete bet:", response.statusText);
            }
        } catch (error) {
            console.error("Error deleting bet:", error);
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
    };

    return (
        <motion.div
            className="bg-white p-6 rounded-2xl shadow-md mt-6"
            initial="hidden"
            animate="visible"
            variants={containerVariants}
        >
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Bet Tracker</h2>
            {bets.length === 0 ? (
                <p className="text-gray-600">No bets tracked yet. Add a bet using the calculator!</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">ID</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Type</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Bookmaker</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Event</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Back Stake</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Back Odds</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Lay Odds</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Lay Stake</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Liability</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Profit/Loss</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {bets.map((bet) => (
                                <motion.tr key={bet.id} variants={itemVariants}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{bet.id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.bet_type}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.bookmaker}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.event_name}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.back_stake}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.back_odds}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.lay_odds}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.lay_stake.toFixed(2)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{bet.liability.toFixed(2)}</td>
                                    <td className={`px-6 py-4 whitespace-nowrap text-sm ${bet.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>{bet.profit_loss.toFixed(2)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <motion.button
                                            onClick={() => handleDeleteBet(bet.id)}
                                            className="text-red-600 hover:text-red-800 transition duration-200 ease-in-out"
                                            whileHover={{ scale: 1.1 }}
                                            whileTap={{ scale: 0.9 }}
                                        >
                                            Delete
                                        </motion.button>
                                    </td>
                                </motion.tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </motion.div>
    );
}

export default BetTrackerTable;